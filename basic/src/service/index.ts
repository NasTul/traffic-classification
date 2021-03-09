import axios from 'axios';

import { UploadResponse, ScanResponse ,FileinfoResponse} from '../type';

const BASE_URL = 'http://121.5.57.180:8788';

export async function uploadFile(file: File, onProgress?: (e: any) => void) {
  const formData = new FormData();
  formData.append('uploadlocation', file);

  const { data } = await axios.post<UploadResponse>(
    `${BASE_URL}/api/uploadfilev2/`,
    formData,
    {
      onUploadProgress(progress) {
        if (onProgress) {
          onProgress({
            percent: (progress.loaded / progress.total) * 100,
          } as any);
        }
      },
    }
  );

  return data;
}
export async function getinfomation (fileinfo: string) {
  const formData = new FormData();
  const basestr = `${BASE_URL}/api/fileinfo/`;
  const ids = fileinfo.toString()
  const src = basestr.concat(ids)
  const { data } = await axios.get<FileinfoResponse>(
    src,
  );

  return data;
}

export async function scanFile(id: string) {
  const formData = new FormData();
  formData.append('ID', id);
  const baseur = `${BASE_URL}/api/getresult/?ID=`
  const src = baseur.concat(id)
  const { data } = await axios.get<ScanResponse>(
    src,
  );

  return data;
}
