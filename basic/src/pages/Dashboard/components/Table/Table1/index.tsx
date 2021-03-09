import React, { FC, useMemo } from 'react';
import { Table } from 'antd';
import { FileinfoResponse} from '../../../../../type';

import 'antd/dist/antd.css';

const COLUMNS = [
  {
    title: 'key',
    dataIndex: 'key',
  },
];

const DEFAULT_DATA = {
  key: 'value',
};
interface FileTableProps {
  data: FileinfoResponse;
}
const FileTable: FC<FileTableProps> = (props) => {
  const { data, columns } = useMemo(() => {

    if (!props.data) {
      return {
        data: [DEFAULT_DATA],
        columns: COLUMNS,
      };
    }

    const keys = Object.keys(props.data);
    const columns = keys.map((k) => ({
      title: k,
      dataIndex: k,
    }));

    return {
      columns: COLUMNS.concat(columns),
      data: [
        {
          ...props.data,
          ...DEFAULT_DATA,
        },
      ],
    };
  }, [props.data]);

  return <Table dataSource={data} columns={columns} pagination={false} />;
};
export default FileTable;


