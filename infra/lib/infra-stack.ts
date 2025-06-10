// infra/lib/infra-stack.ts

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class DjangoAppStack extends cdk.Stack {
  public readonly ecrRepository: ecr.Repository;
  public readonly ecsService: ecs.FargateService;
  public readonly loadBalancer: elbv2.ApplicationLoadBalancer;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Crea un VPC per ospitare l'infrastruttura
    const vpc = new ec2.Vpc(this, 'DjangoAppVpc', {
      maxAzs: 2,
      natGateways: 1
    });

    // Crea un cluster ECS
    const cluster = new ecs.Cluster(this, 'DjangoAppCluster', {
      vpc: vpc
    });

    // Crea un repository ECR per l'immagine Docker
    this.ecrRepository = new ecr.Repository(this, 'DjangoAppRepository', {
      repositoryName: 'django-app',
      removalPolicy: cdk.RemovalPolicy.DESTROY  // Solo per ambiente di sviluppo
    });

    // Crea un secret per le credenziali del database
    const databaseCredentials = new secretsmanager.Secret(this, 'DBCredentials', {
      secretName: 'django-app-db-credentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'postgres' }),
        generateStringKey: 'password',
        excludeCharacters: '/@"'
      }
    });

    // Crea un gruppo di sicurezza per il database
    const databaseSecurityGroup = new ec2.SecurityGroup(this, 'DatabaseSecurityGroup', {
      vpc,
      description: 'Allow database access from the application',
      allowAllOutbound: true
    });

    // Crea un database PostgreSQL
    const database = new rds.DatabaseInstance(this, 'DjangoAppDatabase', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13
      }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_NAT
      },
      securityGroups: [databaseSecurityGroup],
      databaseName: 'djangodb',
      credentials: rds.Credentials.fromSecret(databaseCredentials)
    });

    // Crea un gruppo di sicurezza per l'applicazione
    const appSecurityGroup = new ec2.SecurityGroup(this, 'AppSecurityGroup', {
      vpc,
      description: 'Security group for Django application',
      allowAllOutbound: true
    });

    // Permetti alla app di accedere al database
    databaseSecurityGroup.addIngressRule(
        appSecurityGroup,
        ec2.Port.tcp(5432),
        'Allow application to access database'
    );

    // Crea un task definition per ECS
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'DjangoAppTaskDef', {
      memoryLimitMiB: 1024,
      cpu: 512
    });

    // Aggiungi il container all'ECS task definition
    const container = taskDefinition.addContainer('DjangoContainer', {
      image: ecs.ContainerImage.fromEcrRepository(this.ecrRepository),
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'django-app' }),
      environment: {
        'DATABASE_HOST': database.dbInstanceEndpointAddress,
        'DATABASE_PORT': database.dbInstanceEndpointPort,
        'DATABASE_NAME': 'djangodb',
        'DJANGO_SETTINGS_MODULE': 'backendzero.settings'
      },
      secrets: {
        'DATABASE_USER': ecs.Secret.fromSecretsManager(databaseCredentials, 'username'),
        'DATABASE_PASSWORD': ecs.Secret.fromSecretsManager(databaseCredentials, 'password')
      }
    });

    // Esponi la porta 8000 (Django)
    container.addPortMappings({
      containerPort: 8000
    });

    // Crea un Application Load Balancer
    this.loadBalancer = new elbv2.ApplicationLoadBalancer(this, 'DjangoAppLB', {
      vpc,
      internetFacing: true
    });

    // Crea un target group per il load balancer
    const targetGroup = new elbv2.ApplicationTargetGroup(this, 'DjangoAppTargetGroup', {
      vpc,
      port: 8000,
      protocol: elbv2.ApplicationProtocol.HTTP,
      targetType: elbv2.TargetType.IP,
      healthCheck: {
        path: '/admin/',
        interval: cdk.Duration.seconds(60),
        timeout: cdk.Duration.seconds(5)
      }
    });

    // Aggiungi un listener HTTP al load balancer
    const listener = this.loadBalancer.addListener('HttpListener', {
      port: 80,
      defaultTargetGroups: [targetGroup]
    });

    // Crea un servizio ECS Fargate
    this.ecsService = new ecs.FargateService(this, 'DjangoAppService', {
      cluster,
      taskDefinition,
      desiredCount: 2,
      securityGroups: [appSecurityGroup],
      assignPublicIp: false,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_NAT
      }
    });

    // Registra i task nel target group
    this.ecsService.attachToApplicationTargetGroup(targetGroup);

    // Output utili
    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      value: this.loadBalancer.loadBalancerDnsName,
      exportName: 'DjangoLoadBalancerDNS'
    });

    new cdk.CfnOutput(this, 'RepositoryURI', {
      value: this.ecrRepository.repositoryUri,
      exportName: 'DjangoRepositoryURI'
    });

    new cdk.CfnOutput(this, 'EcsServiceName', {
      value: this.ecsService.serviceName,
      exportName: 'DjangoEcsServiceName'
    });

    new cdk.CfnOutput(this, 'EcsClusterName', {
      value: cluster.clusterName,
      exportName: 'DjangoEcsClusterName'
    });
  }
}