// infra/lib/pipeline-stack.ts

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ecs from 'aws-cdk-lib/aws-ecs';


interface DjangoAppPipelineStackProps extends cdk.StackProps {
    readonly ecrRepository: ecr.Repository;
    readonly ecsService: ecs.FargateService;
    readonly ecsClusterName: string;
    readonly githubOwner: string;
    readonly githubRepo: string;
    readonly githubBranch: string;
    readonly githubTokenSecretName: string;
}

export class DjangoAppPipelineStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props: DjangoAppPipelineStackProps) {
        super(scope, id, props);

        // Artifacts per la pipeline
        const sourceOutput = new codepipeline.Artifact('SourceCode');
        const buildOutput = new codepipeline.Artifact('BuildOutput');

        // Crea un progetto CodeBuild
        const buildProject = new codebuild.PipelineProject(this, 'BuildProject', {
            environment: {
                buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged: true  // Per permettere di creare immagini Docker
            },
            environmentVariables: {
                'REPOSITORY_URI': {
                    value: props.ecrRepository.repositoryUri
                },
                'CLUSTER_NAME': {
                    value: props.ecsClusterName
                },
                'SERVICE_NAME': {
                    value: props.ecsService.serviceName
                }
            },
            buildSpec: codebuild.BuildSpec.fromObject({
                version: '0.2',
                phases: {
                    pre_build: {
                        commands: [
                            'echo Logging in to Amazon ECR...',
                            'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $REPOSITORY_URI',
                            'COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)',
                            'IMAGE_TAG=${COMMIT_HASH:=latest}'
                        ]
                    },
                    build: {
                        commands: [
                            'echo Build started on `date`',
                            'echo Building the Docker image...',
                            'docker build -t $REPOSITORY_URI:latest .',
                            'docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG'
                        ]
                    },
                    post_build: {
                        commands: [
                            'echo Build completed on `date`',
                            'echo Pushing the Docker image...',
                            'docker push $REPOSITORY_URI:latest',
                            'docker push $REPOSITORY_URI:$IMAGE_TAG',
                            'echo Writing image definitions file...',
                            'aws ecs describe-task-definition --task-definition $(aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --query "services[0].taskDefinition" --output text) --query "taskDefinition" > taskdef.json',
                            'echo \'{"ImageURI":"\'$REPOSITORY_URI:$IMAGE_TAG\'"}\'> imageDefinitions.json',
                            'cat imageDefinitions.json'
                        ]
                    }
                },
                artifacts: {
                    files: [
                        'imageDefinitions.json',
                        'taskdef.json',
                        'appspec.yaml'
                    ]
                }
            })
        });

        // Crea un appspec.yaml file durante la fase di build
        buildProject.addToRolePolicy(new iam.PolicyStatement({
            actions: [
                'ecs:DescribeServices',
                'ecs:DescribeTaskDefinition'
            ],
            resources: ['*']
        }));

        // Crea la pipeline
        const pipeline = new codepipeline.Pipeline(this, 'DjangoAppPipeline', {
            pipelineName: 'DjangoAppPipeline'
        });

        // Aggiungi lo stage di source (GitHub)
        pipeline.addStage({
            stageName: 'Source',
            actions: [
                new codepipeline_actions.GitHubSourceAction({
                    actionName: 'GitHub_Source',
                    owner: props.githubOwner,
                    repo: props.githubRepo,
                    branch: props.githubBranch,
                    oauthToken: cdk.SecretValue.secretsManager(props.githubTokenSecretName),
                    output: sourceOutput
                })
            ]
        });

        // Aggiungi lo stage di build
        pipeline.addStage({
            stageName: 'Build',
            actions: [
                new codepipeline_actions.CodeBuildAction({
                    actionName: 'BuildAndPushImage',
                    project: buildProject,
                    input: sourceOutput,
                    outputs: [buildOutput]
                })
            ]
        });

        // Aggiungi lo stage di deploy
        pipeline.addStage({
            stageName: 'Deploy',
            actions: [
                new codepipeline_actions.EcsDeployAction({
                    actionName: 'DeployToECS',
                    service: props.ecsService,
                    input: buildOutput
                })
            ]
        });

        // Concedi i permessi necessari
        props.ecrRepository.grantPullPush(buildProject.role!);
    }
}