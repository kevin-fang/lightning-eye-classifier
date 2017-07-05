cwlVersion: v1.0
class: Workflow
requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: kfang/svc_classify

inputs:
  hiq_tiles:
    type: File
  names:
    type: File
  hiq_info:
    type: File
  assemblyGz:
    type: File
  assemblyFwi:
    type: File

outputs:
  svc_output:
    type: File
    outputSource: classify

steps:
  classify:
    run: classifier.cwl
    output: [svc_output]
