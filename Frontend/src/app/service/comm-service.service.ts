import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class CommServiceService {
  private apiUrl = 'http://127.0.0.1:8000/csrequest/csrequestpage';

  constructor(private http: HttpClient) {}

  fetchItems(category: string | null, page: number): Observable<any> {
    let params = { page: page.toString()};
    if (category) {
      // @ts-ignore
      params['category'] = category;
    }
    return this.http.get(this.apiUrl, { params: params });
  }
}
