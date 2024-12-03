import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as lambda_python from "@aws-cdk/aws-lambda-python-alpha";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as iam from "aws-cdk-lib/aws-iam";
import * as path from "path";
import { Duration } from "aws-cdk-lib";
import { ServicePrincipal } from 'aws-cdk-lib/aws-iam';

export class AgentLambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const layer = new lambda_python.PythonLayerVersion(this, "AgentLayer", {
      entry: path.join(__dirname, "lambda-layer"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
    });
    const myFunction = new lambda.Function(this, "sAgentFunctions", {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "index.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "lambda")),
      layers: [layer],
      timeout: Duration.seconds(10),
      environment: {
        LINE_CHANNEL_ACCESS_TOKEN: "",
        LINE_CHANNEL_SECRET: "",
        AGENT_ID: "ACLX2IUSVN",
        AGENT_ALIAS_ID: "M92G85MO7I"
      }
    })
    // const myFunction = new lambda_python.PythonFunction(this, "AgentFunction", {
    //   entry: path.join(__dirname, "lambda"),
    //   runtime: lambda.Runtime.PYTHON_3_9,
    //   timeout: Duration.seconds(10),
    //   layers: [layer],
    //   environment: {
    //     LINE_CHANNEL_ACCESS_TOKEN: "",
    //     LINE_CHANNEL_SECRET: "",
    //     AGENT_ID: "ACLX2IUSVN",
    //     AGENT_ALIAS_ID: "M92G85MO7I"
    //   }
    // });

    myFunction.grantInvoke(
      new ServicePrincipal('bedrock.amazonaws.com')
    );

    myFunction.addPermission("APIGatewayInvoke", {
      principal: new iam.ServicePrincipal("apigateway.amazonaws.com"),
      action: "lambda:InvokeFunction",
    });

    const api = new apigateway.RestApi(this, "api", {
      restApiName: "api",
      description: "api",
      endpointTypes: [apigateway.EndpointType.EDGE],
      deployOptions: { stageName: "v1" },
    });

    const searchResource = api.root.addResource("search");
    searchResource.addMethod(
      "GET",
      new apigateway.LambdaIntegration(myFunction)
    );
  }
}
