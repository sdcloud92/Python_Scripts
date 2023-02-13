import boto3

cf = boto3.client("cloudformation")

response = cf.create_stack(
    StackName="MyCompanyStack",
    TemplateBody= """
    ---
    
AWSTemplateFormatVersion: 2010-09-09
Resources:
  MycompanyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.10.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      InstanceTenancy: default
  MyCompanyIG:
    Type: AWS::EC2::InternetGateway
    DependsOn: MycompanyVPC
  MyCompanyVPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    DependsOn: 
      - MycompanyVPC
      - MyCompanyIG
    Properties:
      VpcId: !Ref MycompanyVPC
      InternetGatewayId: !Ref MyCompanyIG
  MyRouteTable:
    Type: AWS::EC2::RouteTable
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
    Properties:
      VpcId: !Ref MycompanyVPC
  MyPublicRoute:
    Type: AWS::EC2::Route
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable
    Properties:
      RouteTableId: !Ref MyRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref MyCompanyIG
  companysubnet1:
    Type: AWS::EC2::Subnet
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
    Properties:
      VpcId: !Ref MycompanyVPC
      CidrBlock: 10.10.1.0/24
      AvailabilityZone: us-east-1a
      MapPublicIpOnLaunch: true
  companysubnet2:
    Type: AWS::EC2::Subnet
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
    Properties:
      VpcId: !Ref MycompanyVPC
      CidrBlock: 10.10.2.0/24
      AvailabilityZone: us-east-1b
      MapPublicIpOnLaunch: true
  companysubnet3:
    Type: AWS::EC2::Subnet
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
    Properties:
      VpcId: !Ref MycompanyVPC
      CidrBlock: 10.10.3.0/24
      AvailabilityZone: us-east-1c
      MapPublicIpOnLaunch: true
  MyPublicSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
       - companysubnet1
       - companysubnet2
       - companysubnet3
    Properties:
      RouteTableId: !Ref MyRouteTable
      SubnetId: !Ref companysubnet1
  MyPublicSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
       - companysubnet1
       - companysubnet2
       - companysubnet3
    Properties:
      RouteTableId: !Ref MyRouteTable
      SubnetId: !Ref companysubnet2
  MyPublicSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    DependsOn:
       - MycompanyVPC
       - MyCompanyIG
       - MyCompanyVPCGatewayAttachment
       - MyRouteTable 
       - MyPublicRoute
       - companysubnet1
       - companysubnet2
       - companysubnet3
    Properties:
      RouteTableId: !Ref MyRouteTable
      SubnetId: !Ref companysubnet3
  myCompanySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    DependsOn:
      - MycompanyVPC
    Properties:
      GroupDescription: Allow inbound traffic from HTTP, HTTPS, and SSH
      GroupName: myCompanySecurityGroup
      VpcId: !Ref MycompanyVPC
      SecurityGroupIngress:
        - CidrIp: 0.0.0.0/0
          IpProtocol: tcp
          FromPort: 0
          ToPort: 80
        - CidrIp: 0.0.0.0/0
          IpProtocol: tcp
          FromPort: 0
          ToPort: 443
        - CidrIp: 0.0.0.0/0
          IpProtocol: tcp
          FromPort: 0
          ToPort: 22
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
  MyCompanyWebserver:
    Type: AWS::EC2::LaunchTemplate
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
    Properties:
      LaunchTemplateName: MyCompanyWebserver
      LaunchTemplateData:
        ImageId: ami-0b5eea76982371e91
        InstanceType: t2.micro
        KeyName: AWS_CDA_SERVER_KEYPAIR
        SecurityGroupIds: 
          - !Ref myCompanySecurityGroup
        UserData:
          Fn::Base64:
            !Sub
            #!/bin/bash -xe
            yum update -y
            yum install -y httpd.x86_64
            systemctl start httpd.service
            systemctl enable httpd.service
  MyCompanyASG1:
    Type: AWS::AutoScaling::AutoScalingGroup
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
      - MyCompanyWebserver
    Properties:
      AutoScalingGroupName: MyCompanyASG1
      LaunchTemplate:
        LaunchTemplateId: !Ref MyCompanyWebserver
        Version: !GetAtt MyCompanyWebserver.LatestVersionNumber
      AvailabilityZones:
        - us-east-1a
        - us-east-1b
        - us-east-1c
      MinSize: "2"
      MaxSize: "5"
      DesiredCapacity: "2"
      VPCZoneIdentifier:
        - !Ref companysubnet1
        - !Ref companysubnet2
        - !Ref companysubnet3
  MyCompanyASG1ScalingPolicy:
    Type: AWS::AutoScaling::ScalingPolicy
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
      - MyCompanyWebserver
      - MyCompanyASG1
    Properties:
      AdjustmentType: ChangeInCapacity
      AutoScalingGroupName: !Ref MyCompanyASG1
      PolicyType: TargetTrackingScaling
      TargetTrackingConfiguration:
        DisableScaleIn: false
        PredefinedMetricSpecification:
          PredefinedMetricType: ASGAverageCPUUtilization
        TargetValue: '50'
  MyCompanyALB1:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
      - MyCompanyWebserver
      - MyCompanyASG1
      - MyCompanyASG1ScalingPolicy
    Properties:
      SecurityGroups:
        - !Ref myCompanySecurityGroup
      Subnets:
        - !Ref companysubnet1
        - !Ref companysubnet2
        - !Ref companysubnet3
  ApplicationLoadBalancerTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
      - MyCompanyWebserver
      - MyCompanyASG1
      - MyCompanyASG1ScalingPolicy
      - MyCompanyALB1
    Properties:
      Name: mycompany
      VpcId: !Ref MycompanyVPC
      Port: 80
      Protocol: HTTP
      TargetType: instance
  myCompanyALB1Listener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    DependsOn:
      - MycompanyVPC
      - MyCompanyIG
      - MyCompanyVPCGatewayAttachment
      - MyRouteTable 
      - MyPublicRoute
      - companysubnet1
      - companysubnet2
      - companysubnet3
      - myCompanySecurityGroup
      - MyCompanyWebserver
      - MyCompanyASG1
      - MyCompanyASG1ScalingPolicy
      - MyCompanyALB1
      - ApplicationLoadBalancerTargetGroup
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ApplicationLoadBalancerTargetGroup
      LoadBalancerArn: !Ref MyCompanyALB1
      Port: 80
      Protocol: HTTP
      
""",
)
print(response)