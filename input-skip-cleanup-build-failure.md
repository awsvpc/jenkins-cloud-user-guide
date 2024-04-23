<pre>
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    // Code to create an EC2 instance
                    // Replace this with your actual EC2 creation logic
                    echo 'Creating EC2 instance...'
                    // Example: sh 'aws ec2 run-instances ...'
                }
                script {
                    // User input to determine if cleanup should be skipped
                    def userInput = input(
                        id: 'skipCleanupInput',
                        message: 'Do you want to skip instance cleanup? (Type "approve" to skip)',
                        parameters: [
                            [$class: 'ChoiceParameterDefinition', choices: ['approve', 'reject'], description: 'Choose approve to skip cleanup']
                        ]
                    )

                    // Set environment variable to skip cleanup if approved
                    if (userInput == 'approve') {
                        env.skip_cleanup = 'approved'
                    } else {
                        env.skip_cleanup = 'rejected'
                    }
                }
            }
        }
        stage('Approve') {
            steps {
                script {
                    // Code to perform review/approval
                    // Replace this with your actual approval logic
                    echo 'Reviewing...'
                    // Example: input message: 'Please approve the build', ok: 'Proceed'
                }
            }
        }
    }
    
    post {
        always {
            stage('Cleanup') {
                steps {
                    script {
                        // Check if cleanup should be skipped based on environment variable
                        if (env.skip_cleanup == 'approved') {
                            echo 'Skipping EC2 termination as cleanup was approved...'
                        } else {
                            // Code to terminate the EC2 instance
                            // Replace this with your actual EC2 termination logic
                            echo 'Terminating EC2 instance...'
                            // Example: sh 'aws ec2 terminate-instances ...'
                        }
                    }
                }
            }
        }
    }
}

post {
    failure {
        script {
            // Prompt user for input on failure only if the build stage failed
            if (currentBuild.currentResult == 'FAILURE' && env.STAGE_NAME == 'Build') {
                def userInput = input(
                    id: 'skipCleanupInput',
                    message: 'Do you want to skip instance cleanup? (Type "approve" to skip)',
                    parameters: [
                        [$class: 'ChoiceParameterDefinition', choices: ['approve', 'reject'], description: 'Choose approve to skip cleanup']
                    ]
                )
                
                // Set environment variable to skip cleanup if approved
                if (userInput == 'approve') {
                    env.skip_cleanup = 'approved'
                } else {
                    env.skip_cleanup = 'rejected'
                }
            }
        }
    }
}
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    // Code to create an EC2 instance
                    // Replace this with your actual EC2 creation logic
                    echo 'Creating EC2 instance...'
                    // Example: sh 'aws ec2 run-instances ...'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Code for testing
                    // Simulate a failure for demonstration purposes
                    error('Failure in test stage')
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    // Check if cleanup should be skipped based on environment variable
                    if (env.skip_cleanup == 'approved') {
                        echo 'Skipping EC2 termination as cleanup was approved...'
                    } else {
                        // Code to terminate the EC2 instance
                        // Replace this with your actual EC2 termination logic
                        echo 'Terminating EC2 instance...'
                        // Example: sh 'aws ec2 terminate-instances ...'
                    }
                }
            }
        }
    }
    
    post {
        failure {
            script {
                // Prompt user for input on failure only if the build stage failed
                if (currentBuild.currentResult == 'FAILURE') {
                    def userInput = input(
                        id: 'skipCleanupInput',
                        message: 'Do you want to skip instance cleanup? (Type "approve" to skip)',
                        parameters: [
                            [$class: 'ChoiceParameterDefinition', choices: ['approve', 'reject'], description: 'Choose approve to skip cleanup']
                        ]
                    )
                    
                    // Set environment variable to skip cleanup if approved
                    if (userInput == 'approve') {
                        env.skip_cleanup = 'approved'
                    } else {
                        env.skip_cleanup = 'rejected'
                    }
                }
            }
        }
        always {
            // Post-cleanup block to decide whether to skip or perform termination
            script {
                // Check if cleanup should be skipped based on environment variable
                if (env.skip_cleanup == 'approved') {
                    echo 'Skipping EC2 termination as cleanup was approved...'
                } else {
                    // Code to terminate the EC2 instance
                    // Replace this with your actual EC2 termination logic
                    echo 'Terminating EC2 instance...'
                    // Example: sh 'aws ec2 terminate-instances ...'
                }
            }
        }
    }
}
</pre>
