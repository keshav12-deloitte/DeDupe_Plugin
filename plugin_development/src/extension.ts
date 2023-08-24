import * as vscode from "vscode";
import { sendAPIRequest } from './apiService';
import { getCurrentWorkspaceDirectory, convertStringToJson, convertStringToJson2 } from './commonMethods';
import FormData = require("form-data");




class MethodCodeLensProvider implements vscode.CodeLensProvider {
  provideCodeLenses(document: vscode.TextDocument): vscode.ProviderResult<vscode.CodeLens[]> {
    const methods = this.findMethods(document.getText());
    const codeLenses: vscode.CodeLens[] = [];

    methods.forEach((method: string) => {
      const methodRange = document.getText().indexOf(method);
      const startPosition = document.positionAt(methodRange);
      const endPosition = document.positionAt(methodRange + method.length);

      const range = new vscode.Range(startPosition, endPosition);
      const codeLens1 = new vscode.CodeLens(range);

      //Option 1 (DeDupe this file)
      codeLens1.command = {
        title: "DeDupe File : " + method,
        command: "duplicatechecker.option1",
        arguments: [method],
      };

      //Option 2 (DeDupe this repo)
      const codeLens2 = new vscode.CodeLens(range);
      codeLens2.command = {
        title: "DeDupe Repo",
        command: "duplicatechecker.option2",
        arguments: [method],
      };

      codeLenses.push(codeLens1, codeLens2);
    });

    return codeLenses;
  }

  resolveCodeLens(codeLens: vscode.CodeLens): vscode.ProviderResult<vscode.CodeLens> {
    return codeLens;
  }

  findMethods(text: string): string[] {
    const methodRegex = /def\s+(\w+)\s*\(/g;
    const methods: string[] = [];
    let match: RegExpExecArray | null;

    while ((match = methodRegex.exec(text)) !== null) {
      const methodName = match[1];
      methods.push(methodName);
    }

    return methods;
  }
  findMethodCode(text: string, methodName: string): string | undefined {
    const methodRegex = new RegExp(`def\\s+${methodName}\\s*\\(`);
    const methodMatch = methodRegex.exec(text);
    if (methodMatch) {
      const methodStartIndex = methodMatch.index;
      const methodEndIndex = text.indexOf("\n\n", methodStartIndex);
      const methodCode = text.substring(methodStartIndex, methodEndIndex !== -1 ? methodEndIndex : undefined);
      return methodCode;
    }
    return undefined;
  }
}


export function activate(context: vscode.ExtensionContext) {
  console.log("Plugin activated");
  const codeLensProvider = new MethodCodeLensProvider();
  context.subscriptions.push(vscode.languages.registerCodeLensProvider("*", codeLensProvider));


  // Handling DeDupe file search (Option 1)
  vscode.commands.registerCommand("duplicatechecker.option1", (methodName: string) => {
    let responseData: any;
    let formattedData: any;
    vscode.window.showInformationMessage(`Clicked on method: ${methodName}`);
    const editor = vscode.window.activeTextEditor;
    if (editor) {
      const document = editor.document;
      const methodCode = codeLensProvider.findMethodCode(document.getText(), methodName);
      if (methodCode) {
        const panel = vscode.window.createWebviewPanel(
          "Method_Name_" + methodName, // Unique identifier for the panel
          "DeDupe : " + methodName, // Title displayed in the panel
          vscode.ViewColumn.Beside, // Panel is shown in the first column of the editor
          {}
        );

        if (editor) {
          panel.webview.html += `<h1>DeDupe File</h1>`;

          // Send a POST request to the API
          const fullFileCode = editor.document.getText();
          const apiUrl = 'http://127.0.0.1:8000/DeDupeForFile/';
          const contentTYPE = 'multipart/form-data';
          const formData = new FormData();
          formData.append('code_string1', fullFileCode);
          formData.append('code_string2', methodCode);
          // Send post request
          sendAPIRequest(apiUrl, 'POST', undefined, formData, undefined, undefined, contentTYPE)
            .then((response) => {
              if (panel) {
                if (response.status === 200) {
                  responseData = JSON.stringify(response.data, null, 2);
                  console.log("--------------------------RESPONSE DATA --------------------------------");
                  console.log(response.data);
                  console.log("----------------------------------------------------------");
                  formattedData = responseData.split('\\n').join('\n');
                  console.log("--------------------------FORMATTED DATA --------------------------------");
                  console.log(formattedData);
                  console.log("----------------------------------------------------------");
                  let beautifyData = convertStringToJson2(formattedData);
                  console.log("--------------------------BEAUTIFUL CODE --------------------------------");
                  console.log(beautifyData);
                  console.log("----------------------------------------------------------");
                  const data = JSON.parse(beautifyData);
                  // Constructing the HTML content
                  let htmlContent = '';
                  for (const entry of data) {
                    const methodName = entry["method name"];
                    htmlContent += `<div>
                <h2>Method Name: ${methodName}</h2>
                <div>`;

                    const similarCodeArray = entry["similar code"];
                    htmlContent += "<p>Similar code:</p>";

                    for (const similarCodeEntry of similarCodeArray) {
                      const className = similarCodeEntry["Class Name"];
                      const similarCode = similarCodeEntry["Similar code"];

                      htmlContent += `
                <div style="border: 1px solid white; margin-top: 20px; ">
                    <p>---------The above method is duplicated in the below-mentioned file, please check it -----------</p>
                    ${generateIframeContent(className, similarCode)}
                </div>`;
                    }
                    htmlContent += `</div></div>`;
                  }
                  panel.webview.html += htmlContent;

                  function generateIframeContent(className: string, similarCode: string): string {
                    return `
            <ol>
              <li><p style="color:#8A2BE2;">Class Name: ${className}</p></li>
              <li><p style="color:#8A2BE2;">Similar code: ${similarCode}</p></li>
            </ol>
            <script>
              function openFile(uri) {
                vscode.postMessage({
                  command: 'openFile',
                  text: uri
                });
              }
            </script>
          `;
                  }
                }
              }
            })
            .catch((error) => {
              console.error('Error:', error);
              if (panel) {
                panel.webview.html += `
      <h3>We are in error block a</h3>
      <h3>${error}</h3>
      `;

              }
            });

        }


      }
    }
  });


  // Handling DeDupe Repo search (Option 2)
  vscode.commands.registerCommand("duplicatechecker.option2", (methodName: string) => {
    let responseData: any;
    let formattedData: any;
    vscode.window.showInformationMessage(`Clicked on Option 2 for method: ${methodName}`);
    // Add your custom logic for Option 2 here
    // Get full text
    const editor = vscode.window.activeTextEditor;
    const panel = vscode.window.createWebviewPanel(
      "Method_Name_" + methodName, // Unique identifier for the panel
      "DeDupeRepo : " + methodName, // Title displayed in the panel
      vscode.ViewColumn.Beside, // Panel is shown in the first column of the editor
      {}
    );
    if (editor) {
      // Get full text
      const fullFileCode = editor.document.getText();
      panel.webview.html += `<h1 style="color:#FFFFFF;text-align:center;" >DE-Dupe :The Duplicate Checker</h1>
      <h2 style="color:#00CC66;text-align:center;" >Welcome to our AI Tool called DE-Dupe which helps many software engineers to come out from the loop
      of finding duplicate code in their code base,Dont worry we are here to help you </h2>`;
      // Set the HTML content of the panel
      // panel.webview.html += `<pre><code>${methodCode}</code></pre>`;
      // panel.webview.html += `<pre><code>${fullFileCode}</code></pre>`;

      // Send a POST request to the API
      const apiUrl = 'http://127.0.0.1:8000/DeDupeForRepo/';
      const contentTYPE = 'multipart/form-data';
      const formData = new FormData();
      formData.append('code_string', fullFileCode);
      // Send post request
      sendAPIRequest(apiUrl, 'POST', undefined, formData, undefined, undefined, contentTYPE)
        .then((response) => {
          // Display the analysis results and API response in the webview panel
          if (panel) {
            panel.webview.postMessage({ command: 'hideLoadingGif' }); // Notify the webview to hide the loading GIF
            // panel.webview.
            if (response.status === 200) {
              responseData = JSON.stringify(response.data, null, 2);
              const formattedData = responseData.split('\\n').join('\n');
            }
            else {
              panel.webview.html += `<h3>We support only Python</h3>`;

            }

            let beautifyData = convertStringToJson(formattedData);

            const data = JSON.parse(beautifyData);
            // Constructing the HTML content
            let htmlContent = '';
            for (const entry of data) {
              const methodName = entry["method name"];
              htmlContent += `<div>
                <h2>Method Name: ${methodName}</h2>
                <div>`;

              const similarCodeArray = entry["similar code"];
              htmlContent += "<p>Similar code:</p>";

              for (const similarCodeEntry of similarCodeArray) {
                const fileName = similarCodeEntry["File Name"];
                const className = similarCodeEntry["Class Name"];
                const similarCode = similarCodeEntry["Similar code"];

                htmlContent += `
                <div style="border: 1px solid white; margin-top: 20px; ">
                    <p>---------The above method is duplicated in the below-mentioned file, please check it -----------</p>
                    ${generateIframeContent(fileName, className, similarCode)}
                </div>`;
              }
              htmlContent += `</div></div>`;
            }
            panel.webview.html += htmlContent;

            function generateIframeContent(fileName: string, className: string, similarCode: string): string {
              return `
            <ol>
              <li><p style="color:#8A2BE2;">File Name:>${fileName}</a></p></li>
              <li><p style="color:#8A2BE2;">Class Name: ${className}</p></li>
              <li><p style="color:#8A2BE2;">Similar code: ${similarCode}</p></li>
            </ol>
            <script>
              function openFile(uri) {
                vscode.postMessage({
                  command: 'openFile',
                  text: uri
                });
              }
            </script>
          `;
            }
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          if (panel) {
            panel.webview.html += `
      <h3>We are in error block a</h3>
      <h3>${error}</h3>
      `;

          }
        });
    }


  });
}



export function deactivate() { }