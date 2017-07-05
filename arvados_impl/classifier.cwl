cwlVersion: v1.0
class: CommandLineTool
requirements:
  InlineJavascriptRequirement: {}
hints:
  DockerRequirement:
    dockerPull: kfang/svc_classify
stdout: $("svc_classified")
baseCommand: ["./run_left_classify_arv.py"]
inputs:
  hiq_tiles:
    type: File
    inputBinding:
      position: 1
  names:
    type: File
    inputBinding:
      position: 2
  hiq_info:
    type: File
    inputBinding:
      position: 3
  assemblyGz:
    type: File
    inputBinding:
      position: 4
  assemblyFwi:
    type: File
    inputBinding:
      position: 5
    
