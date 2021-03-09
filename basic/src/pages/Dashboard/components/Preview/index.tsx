import React, { FC , useState } from 'react';
import { Button } from 'antd';
import { ScanResponse } from '../../../../type';
import { parseQuery } from '../../../../utils/browser';
import './index.css';
interface PreviewProps {
  data: ScanResponse;
}

const BASE_URL = 'http://121.5.57.180:8788/api/uploadfile/';
const Preview: FC<PreviewProps> = (props) => {
  const { label_graphid: lid, unlabel_graphid: ulid } = props.data;
  window.history.pushState(
    {},
    "tryonce",
    `${window.location.pathname}?lid=${lid}&ulid=${ulid}`
  );
  const [on,setOn] = useState(false);
  const [on1,setOn1] =useState(false);
  if (!lid || !ulid) {
    return null;
  }
  const show = () => setOn(true)
  const show1 = () => setOn1(true)
  const element1 = (          
  <iframe
    className="preview-iframe"
    title="iframe"
    src="unabledgraph.html"
  ></iframe>)
  const element2 = (
    <iframe
    className="preview-iframe"
    title="iframe"
    src="labeledgraph.html"
  ></iframe>  
  )
  return (
    <div className="preview">
        <div className="preview-item">
          {/* <div className="preview-title">Unlabeled</div> */}
          <div className = "clickbutton1" >
                <Button onClick={show}>Show Unlabeled Graph
                </Button>
          </div>
          {on ? (element1):null}
          
        </div>

        <div className="preview-divider" />
            <div className="preview-item">
              {/* <div className="preview-title">Labeled</div> */}
              <div className = "clickbutton" >
              <Button onClick={show1}>Show Labeled Graph
                </Button>
              </div>
              {on1 ? (element2):null}
            </div>
    </div>
  );
};

export default Preview;
