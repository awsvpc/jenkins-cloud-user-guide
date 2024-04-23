pipeline {
    agent any

    stages {
        stage('Run Playbook on EC2 Instance') {
            steps {
                script {
                    def instanceId = "i-123124242424"
                    def playbookName = "your_playbook.yml"
                    def region = "us-east-1" // Update with your desired region
                    
                    // Step 1: Start Session Manager
                    def startSessionCmd = "aws ssm start-session --target ${instanceId} --region ${region}"
                    sh startSessionCmd

                    // Step 2: Upload playbook to the EC2 instance
                    def uploadCmd = "aws s3 cp ${playbookName} ssm://${instanceId}/tmp/${playbookName} --region ${region}"
                    sh uploadCmd

                    // Step 3: Execute playbook on the EC2 instance
                    def executeCmd = "aws ssm send-command --document-name AWS-RunShellScript --targets Key=instanceids,Values=${instanceId} --parameters 'commands=bash /tmp/${playbookName}' --region ${region}"
                    sh executeCmd
                }
            }
        }
    }
}
