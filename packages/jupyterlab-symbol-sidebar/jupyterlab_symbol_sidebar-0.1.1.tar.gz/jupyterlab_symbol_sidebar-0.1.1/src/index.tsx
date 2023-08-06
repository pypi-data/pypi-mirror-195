import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILabShell
} from '@jupyterlab/application';

import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';

import {codeList} from './code';

/**
 * Initialization data for the jupyterlab-sidepanel extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'TESTEX:plugin',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('JupyterLab extension TESTEX is activated!');

    const newWidget = () => {
      // Create a blank content widget inside of a MainAreaWidget
      const widget = ReactWidget.create(
        <MyComponent />
      );
      //const widget = new MainAreaWidget({ content });
      widget.id = 'symbols-jupyterlab';
      widget.title.label = 'Symbols';
      widget.title.closable = true;
      return widget;
    }
    let widget = newWidget();

    // let summary = document.createElement('p');
    // widget.node.appendChild(summary);
    // summary.innerText = "Hello, World!";

    shell.add(widget, 'left');
  }
};

function MyComponent() {
  var list = codeList;

  return (
    <div className="sidebar-container">
      <div className="notice">Click on icon will copy to clipboard</div>
          <div className="block_container">
            {list.map((item,i) => 
              <div 
                key={i} 
                onClick={() => iconClick(item.unicode)}
              >
                {item.unicode}
                <div>{item.name}</div>
              </div>)}
          </div>
    </div>
    );
}

function iconClick(code:any) {
  //JSON.parse(`["${item.unicode}"]`)[0].toString()
  navigator.clipboard.writeText(JSON.parse(`["`+code+`"]`)[0].toString())
                   
}

export default extension;
