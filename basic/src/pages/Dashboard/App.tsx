import React, { useState } from 'react';
import { Layout, Menu, Breadcrumb, Upload, Divider, Spin, message,Button } from 'antd';
import { useRequest } from 'ahooks';
import { InboxOutlined, ReloadOutlined } from '@ant-design/icons';

import Table from './components/Table';
import Table1 from "./components/Table/Table1"
import Preview from './components/Preview';

import { uploadFile, scanFile, getinfomation} from '../../service/index';
import { parseQuery } from '../../utils/browser';

import logo from '../../assets/logo.svg';

import './App.css';
import 'antd/dist/antd.css';

const { Header, Content, Footer } = Layout;
const { Dragger } = Upload;

interface Query {
  gid?: string;
  id?: string;
  fileinfo?:string;
}

function App() {
  const [query, setQuery] = useState(() => parseQuery<Query>());
  const { id, gid , fileinfo} = query;
  const { data: nodeinfos, run: getinfo} = useRequest(() =>
  fileinfo
    ? getinfomation(fileinfo).catch(() => message.error('Get node res failed'))
    : Promise.resolve()
)

  const { data: scanRes, error, run: scan, loading } = useRequest(() =>
    id
      ? scanFile(id).catch(() => message.error('Get scanFile res failed'))
      : Promise.resolve()
  )
  
  ;

  return (
    <Layout className="container">
      <Header className="header">
        <img className="logo" src={logo} alt="here is logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1">Dashboard</Menu.Item>
        </Menu>
      </Header>
      <Content className="content" style={{ padding: '0 50px', marginTop: 64 }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
        </Breadcrumb>
        <div className="main">
          <Dragger
            accept=".csv"
            customRequest={async ({ file, onProgress, onSuccess, onError }) => {
              try {
                const {
                  graphid,
                  msg: { ID },
                  fileinfoid
                } = await uploadFile(file, onProgress);

                if (onSuccess) {
                  onSuccess(null, new XMLHttpRequest());
                }

                window.history.pushState(
                  {},
                  file.name,
                  `${window.location.pathname}?gid=${graphid}&id=${ID}&datainfo=${fileinfoid}`
                );

                setQuery({
                  gid: graphid.toString(),
                  id: ID.toString(),
                  fileinfo:fileinfoid.toString()
                });
                getinfo()
                scan();
              } catch (e) {
                if (onError) {
                  onError(new Error('Upload failed'));
                }
              }
            }}
            onChange={(info) => {
              const { status } = info.file;
              if (status !== 'uploading') {
                console.log(info.file, info.fileList);
              }
              if (status === 'done') {
                message.success(
                  `${info.file.name} file uploaded successfully.`
                );
              } else if (status === 'error') {
                message.error(`${info.file.name} file upload failed.`);
              }
            }}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
            <p className="ant-upload-hint">Only .csv file is allowed</p>
          </Dragger>

          <Divider />
          <div className="nodeinfo">
            <div className="nodetitle">Dataset Description</div>
            {nodeinfos ? (
              <Table1 data={nodeinfos} />
            ) : (
              <div className="noderesult">
                {loading ? <Spin size="large" /> : null}
                {!loading && error ? (
                  <ReloadOutlined className="reload" onClick={getinfo} />
                ) : null}
              </div>
            )}
          </div>

          <div className="dashboard">
            <div className="title"> Anomaly Detection Result</div>
            {scanRes ? (
              <Table data={scanRes} />
            ) : (
              <div className="result">
                {loading ? <Spin size="large" /> : null}
                {!loading && error ? (
                  <ReloadOutlined className="reload" onClick={scan} />
                ) : null}
              </div>
            )}
            
            {scanRes ? <Preview data={scanRes} /> : null}
          </div>
        </div>
      </Content>
      <Footer className="footer">Here is Footer</Footer>
    </Layout>
  );
}

export default App;
