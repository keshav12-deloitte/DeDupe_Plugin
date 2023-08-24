import * as path from 'path';
import * as fs from 'fs';

export function getCurrentWorkspaceDirectory(): string | null {
  let currentDirectory = path.resolve(process.cwd());
  let workspaceDirectory: string | null = null;

  while (currentDirectory !== null && !fs.existsSync(path.join(currentDirectory, '*.sln'))) {
    currentDirectory = path.dirname(currentDirectory);
  }

  if (currentDirectory !== null) {
    workspaceDirectory = currentDirectory;
  }

  return workspaceDirectory;
}


export function convertStringToJson(str: string) {
  const lines = str.split('\n');
  const result = [];
  let currentMethod : any;

  for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith('Method name')) {
          if (currentMethod) {
              result.push(currentMethod);
          }

          currentMethod = {
              'method name': line.split('=')[1].trim(),
              'similar code': []
          };
      } else if (line.startsWith('File Name')) {
          const similarCode = {
              'File Name': line.split('=')[1].trim(),
              'Class Name': lines[++i].split('=')[1].trim(),
              'Similar code': lines[++i].split('=')[1].trim()
          };

          currentMethod['similar code'].push(similarCode);
      }
  }

  if (currentMethod) {
      result.push(currentMethod);
  }

  return JSON.stringify(result, null, 2);
}


export function convertStringToJson2(str: string): string {
  const lines: string[] = str.split('\n');
  const result: any[] = [];
  let currentMethod: any;

  for (let i = 0; i < lines.length; i++) {
    const line: string = lines[i].trim();

    if (line.startsWith('Similar Code')) {
      if (currentMethod) {
        result.push(currentMethod);
      }

      const classNameLine: string = lines[i + 1];
      const className: string = classNameLine.split('=')[1].trim();

      currentMethod = {
        'Similar Code': line.split(':')[1].trim(),
        'Class Name': className,
        'Code': []
      };
    } else if (line.startsWith('Similar Code =')) {
      currentMethod['Code'].push(line.split('=')[1].trim());
    }
  }

  if (currentMethod) {
    result.push(currentMethod);
  }

  return JSON.stringify(result, null, 2);
}

