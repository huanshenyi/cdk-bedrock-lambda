#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { AgentLambdaStack } from '../lib/agent_lambda-stack';

const app = new cdk.App();
new AgentLambdaStack(app, 'AgentLambdaStack', {});