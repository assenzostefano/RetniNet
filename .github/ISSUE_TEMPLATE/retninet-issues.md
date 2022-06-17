---
name: 🔴 RetniNet Issues
about: Before opening an issue on Github, make sure your problem has not already been
  fixed.
title: BUG
labels: [bug]
body:
  - type: checkboxes
    id: no-duplicate-issues
    attributes:
      label: "⚠️ Please verify that this bug has NOT been reported before."
      description: "Search in the issues sections by clicking [HERE](https://github.com/assenzostefano/RetniNet"
      options:
        - label: "I checked all existing issues and didn't find a similar issue"
          required: true
  - type: textarea
    id: description
    validations:
      required: false
    attributes:
      label: "Description"
      description: "You could also upload screenshots, if necessary"
  - type: textarea
    id: steps-to-reproduce
    validations:
      required: true
    attributes:
      label: "👟 Reproduction steps"
      description: "How do you trigger this bug? Please walk us through the problem, step by step"
      placeholder: "..."
  - type: textarea
    id: expected-behavior
    validations:
      required: true
    attributes:
      label: "👀 Expected behavior"
      description: "What did you think would or should happen?"
      placeholder: "..."
  - type: textarea
    id: actual-behavior
    validations:
      required: true
    attributes:
      label: "😓 Actual Behavior"
      description: "What actually happen?"
      placeholder: "..."
  - type: input
    id: brayanbot-version
    attributes:
      label: ":robot: BrayanBot Version" 
      description: 'Which version of BrayanBot are you running? Please do NOT provide the docker tag. Do remember that "latest" is not a version.'
      placeholder: "Ex. 1.10.0"
    validations:
      required: true
  - type: input
    id: operating-system
    attributes:
      label: "💻 Operating System and Arch"
      description: "Which OS is your server/device running on?"
      placeholder: "Ex. Ubuntu 20.04 x86"
    validations:
      required: true
  - type: input
    id: nodejs-version
    attributes:
      label: "🟩 NodeJS Version"
      description: "What version of NodeJS are you running?"
      placeholder: "Ex. v16.3.2"
    validations:
      required: true
  - type: input
    id: docker-version
    attributes:
      label: "🐋 Docker Version"
      description: "If running with Docker, which version are you running?"
      placeholder: "Ex. Docker 20.10.9 / K8S / Podman"
    validations:
      required: false
  - type: textarea
    id: logs
    attributes:
      label: "📝 Relevant log output"
      description: Please copy and paste any relevant log output. This will be automatically formatted into code, so no need for backticks.
      render: shell
    validations:
      required: true
