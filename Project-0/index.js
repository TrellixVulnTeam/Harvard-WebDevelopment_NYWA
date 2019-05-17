import React from "react";
import ReactDOM from "react-dom";
import { version, Button } from "antd";
import "antd/dist/antd.css";
import "./index.css";

import { Button } from 'antd';

ReactDOM.render(
  <div classname="ant-btn">
    <Button type="primary">Primary</Button>
    <Button>Default</Button>
    <Button type="dashed">Dashed</Button>
    <Button type="danger">Danger</Button>
    <Button type="link">Link</Button>
  </div>,
  mountNode
);