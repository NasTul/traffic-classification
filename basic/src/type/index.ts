export interface UploadResponse {
  msg: {
    ID: number;
    uploadlocation: string;
  },
  graphid: number,
  fileinfoid:string
}

export interface ScanResponse {
  result_dict: {
    acc: number;
    fpr: number;
    fnr: number;
    rec: number;
    prc: number;
    f1: number;
    auroc: number;
  },
  label_graphid: number;
  unlabel_graphid: number;
}

export interface FileinfoResponse {
  id:number;
  node_numbers:number;
  edges_numbers:number;
  anomalous_ndoes: number;
  anomalous_edges: number;
}