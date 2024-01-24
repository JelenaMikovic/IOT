import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  public alarm: boolean = false
  public numb: string = '';
  private pin: string = "4507"


  constructor(private socket: Socket, private http: HttpClient) { }

  ngOnInit(): void {
    this.socket.on('alarm', (data: string) => {
      console.log('Alarm status:', data);
      if(data == "on"){
        this.alarm = true
      } else {
        this.alarm = false
      }
    });
  }

  updateNumber(digit: string): void {
    if(this.numb.length < 4){
      this.numb += digit;
    }
  }

  onGoClick(): void {
    if(this.numb != this.pin){
      alert("Pin is not correct")
    }
    else{
      this.numb = '';
      this.http.get('http://localhost:5000/alarm').subscribe(
        (response: any) => {
          console.log('Alarm turned off successfully:', response);
        },
        (error: any) => {
          console.error('Error turning off alarm:', error);
        }
      );
    }
  }

  onDeleteClick(): void {
    this.numb = this.numb.slice(0, -1);
  }


}
