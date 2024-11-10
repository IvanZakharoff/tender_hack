import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

interface Session {
  URL: string;
  rules: number[];
}

interface SessionFiles {
  URL: string;
  tzFile: File;
  contractFile: File;
}

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {
  private apiUrl = 'http://localhost:5003/check_sessions';

  constructor(private http: HttpClient) { }

  uploadData(sessions: Session[], filesData: SessionFiles[]): Observable<any> {
    const formData = new FormData();

    const formattedData = {
      cs_list: sessions.map(session => ({
          url: session.URL,
          rules: session.rules
      }))
  };

    formData.append('data', JSON.stringify(formattedData));

    filesData.forEach((UrlFiles) => {
      if (UrlFiles.tzFile) { 
        const tzFileExtension = UrlFiles.tzFile.name.split('.').pop(); // Получаем расширение файла 
        formData.append(UrlFiles.URL, UrlFiles.tzFile, `tz.${tzFileExtension}`); 
      } 
      if (UrlFiles.contractFile) { 
        const contractFileExtension = UrlFiles.contractFile.name.split('.').pop(); // Получаем расширение файла 
        formData.append(UrlFiles.URL, UrlFiles.contractFile, `contract.${contractFileExtension}`); 
      }

    });

    
    return this.http.post(this.apiUrl, formData);
  }
}
