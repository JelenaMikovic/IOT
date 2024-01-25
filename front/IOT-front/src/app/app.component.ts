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
  public alarmClock: boolean = false;
  public numb: string = '';
  private pin: string = "4507"
  public selectedMode: string = 'off';

  selectedHour: string = "00";
  selectedMinute: string = "00";

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

    this.socket.on('alarmClock', (data: string) => {
      console.log('Alarm clock status:', data);
      if(data == "clockOn"){
        console.log("UKLJUCEN ALARM ZA BUDJENJE!!!!!!")
        this.alarmClock = true
      } else {
        this.alarmClock = false
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

  onChangeMode(): void {
    this.http.post('http://localhost:5000/rgb', { mode: this.selectedMode }).subscribe(
      (response: any) => {
        console.log(`RGB mode set to: ${this.selectedMode}`);
      },
      (error: any) => {
        console.error('Error setting RGB mode:', error);
      }
    );
  }

  addAlarmCLock():void{
    let time = this.selectedHour + ":" + this.selectedMinute;
    console.log(time);
    this.http.post('http://localhost:5000/addAlarmClock', { req : time }).subscribe(
      (response: any) => {
        console.log(`Alarm clock set to : ${time}`);
      },
      (error: any) => {
        console.error('Error setting RGB mode:', error);
      }
    );
  }


  turnOffAlarmClock(): void{
    this.http.get('http://localhost:5000/alarmClockOff').subscribe(
      (response: any) => {
        console.log('Alarm clock turned off successfully:', response);
      },
      (error: any) => {
        console.error('Error turning off alarm:', error);
      }
    );
  }

}
