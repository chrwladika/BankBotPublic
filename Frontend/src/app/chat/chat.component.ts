import { Component } from '@angular/core';
import { HttpClient } from "@angular/common/http";

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent {
  message: string = '';
  responses: string[] = [];
  disabledButton: boolean = false;

  constructor(private http: HttpClient) { }

  /**
   * Sends a chat message and receives a response from the server.
   */
  sendMessage() {
    this.responses.push(this.message)
    this.disabledButton = true;
    this.http.post('http://127.0.0.1:8000/csrequest/chat/1', { message: this.message }).subscribe(
      (data: any) => {
        this.responses.push(data.response);
        this.message = "";
        this.disabledButton = false;
      },
      error => {
        console.error("There was an error!", error);
        this.responses.pop();
        this.message = "";
        this.disabledButton = false;
      }
    );
  }

  getAlignment(index: number): string {
    return index % 2 === 0 ? 'chat-right' : 'chat-left';
  }

  getAlignmentImage(index: number): string {
    return index % 2 === 0 ? 'chat-avatar-right' : 'chat-avatar-left';
  }

}
