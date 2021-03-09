import React, { FC, useMemo } from 'react';
import { Table } from 'antd';
import { ScanResponse} from '../../../../type';

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

interface ScanTableProps {
  data: ScanResponse;
}

const ScanTable: FC<ScanTableProps> = (props) => {
  const { data, columns } = useMemo(() => {
    const { result_dict: dict } = props.data;

    if (!dict) {
      return {
        data: [DEFAULT_DATA],
        columns: COLUMNS,
      };
    }

    const keys = Object.keys(dict);
    const columns = keys.map((k) => ({
      title: k,
      dataIndex: k,
    }));

    return {
      columns: COLUMNS.concat(columns),
      data: [
        {
          ...dict,
          ...DEFAULT_DATA,
        },
      ],
    };
  }, [props.data]);

  return <Table dataSource={data} columns={columns} pagination={false} />;
};

export default ScanTable;
