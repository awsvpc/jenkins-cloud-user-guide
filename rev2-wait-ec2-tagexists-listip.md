pipeline {
    agent any
    
    stages {
        stage('Wait for EC2 Tag') {
            steps {
                script {
                    def instanceId = 'i-12313131313'
                    def timeout = 30 * 60 // 30 minutes in seconds
                    def interval = 5 * 60 // 5 minutes in seconds
                    def startTime = currentBuild.startTimeInMillis
                    
                    timeout(time: timeout, unit: 'SECONDS') {
                        while (true) {
                            def tagValue = sh(script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[*].Instances[*].Tags[?Key==`Deploy`].Value' --output text", returnStdout: true).trim()
                            if (tagValue == 'complete') {
                                break
                            }
                            def elapsedTime = (currentBuild.startTimeInMillis - startTime) / 1000
                            if (elapsedTime >= timeout) {
                                error "Timeout reached while waiting for EC2 tag"
                            }
                            echo "Waiting for EC2 tag 'Deploy' with value 'complete'..."
                            sleep interval
                        }
                    }
                }
            }
        }
        
        stage('Check and Retrieve Management IP') {
            steps {
                script {
                    def instanceId = 'i-12313131313'
                    def eniIds = sh(script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[*].Instances[*].NetworkInterfaces[*].NetworkInterfaceId' --output text", returnStdout: true).trim().split('\n')
                    def managementIpFound = false
                    def managementIp
                    
                    for (eniId in eniIds) {
                        def subnetId = sh(script: "aws ec2 describe-network-interfaces --network-interface-ids ${eniId} --query 'NetworkInterfaces[*].SubnetId' --output text", returnStdout: true).trim()
                        def tierTag = sh(script: "aws ec2 describe-subnets --subnet-ids ${subnetId} --query 'Subnets[*].Tags[?Key==`tier`].Value' --output text", returnStdout: true).trim()
                        
                        if (tierTag == 'mgt') {
                            managementIp = sh(script: "aws ec2 describe-network-interfaces --network-interface-ids ${eniId} --query 'NetworkInterfaces[*].PrivateIpAddresses[0].PrivateIpAddress' --output text", returnStdout: true).trim()
                            managementIpFound = true
                            break
                        }
                    }
                    
                    if (!managementIpFound) {
                        error "Management IP not found"
                    }
                    
                    writeFile file: 'inventory.txt', text: "[default]\n${managementIp}"
                }
            }
        }
    }
}
