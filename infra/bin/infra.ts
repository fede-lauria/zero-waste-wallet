#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DjangoAppStack } from '../lib/infra-stack';
import { DjangoAppPipelineStack } from '../lib/pipeline-stack';

const app = new cdk.App();

// Deploy dell'infrastruttura principale
const djangoStack = new DjangoAppStack(app, 'DjangoAppStack');

// Deploy della pipeline CI/CD
new DjangoAppPipelineStack(app, 'DjangoAppPipelineStack', {
    ecrRepository: djangoStack.ecrRepository,
    ecsService: djangoStack.ecsService,
    ecsClusterName: cdk.Fn.importValue('DjangoEcsClusterName'),
    githubOwner: 'fede-lauria',  // Sostituisci con il tuo username GitHub
    githubRepo: 'zero-waste-wallet',        // Sostituisci con il nome del tuo repository
    githubBranch: 'main',                // Sostituisci con il tuo branch principale
    githubTokenSecretName: 'github-token'
});

app.synth();