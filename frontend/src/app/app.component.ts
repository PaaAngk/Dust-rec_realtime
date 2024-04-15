import { TuiRootModule, TuiDialogModule, TuiAlertModule } from "@taiga-ui/core";
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { VideoComponent } from './video/video.component';
// import { Redis } from "ioredis"
import { CommonModule } from '@angular/common';
import { TableComponent } from "./table/table.component";
// import * as zmq from "zeromq"


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    CommonModule,
    VideoComponent,
    TableComponent,

    TuiRootModule,
    TuiDialogModule,
    TuiAlertModule,
    TuiRootModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.less'
})
export class AppComponent {
  wsConnect = false;
  loading = true;
  isAlarm = false;
  objectsCount = null;
  videoList = [
    "http://localhost:888/stream/city-traffic/index.m3u8",
    "http://localhost:888/stream/city-traffic/index.m3u8"
  ]

  constructor() {}

  async ngOnInit() {
    
    this.connect()
    // await this.client.connect();
    // const subscriber = this.client.duplicate();
    // subscriber.on('error', (err: any) => console.log('Redis Client Error', err));
    // const listener = (message: any, channel: any) => console.log(message, channel);

    // subscriber.sSubscribe("test-source", listener);
    // const redis = new Redis({
    //   port: Number(6379),
    //   host: "localhost",
    // });
    // const socket = io('http://localhost:5002', {
    //   extraHeaders: {
    //     "Access-Control-Allow-Origin": "*"
    //   }
    // });
    // socket.on("connect", () => {
    //   console.log(socket.id); // x8WIv7-mJelg7on_ALbx
    // });
    
    // socket.on("disconnect", () => {
    //   console.log(socket.id); // undefined
    // });

    // socket.on('message', function (data) {
    //   console.log("data", data)
    // });    
    
    // async function run() {
    //   const sock = new zmq.Subscriber()
    //   console.log("Subscriber connected to port 5555")

    //   sock.connect("tcp://127.0.0.1:5555")
    //   sock.subscribe()
    
    //   for await (const [topic, msg] of sock) {
    //     console.log("received a message related to:", topic, "containing message:", msg)
    //   }
    // }
    // run()
  }

  connect() {
    let ws = new WebSocket('ws://localhost:8000/ws');
    ws.onopen = () => {
      this.wsConnect = true;
      this.loading = false; 
    }
  
    ws.onmessage = (e) => {
      let data = JSON.parse(e.data);
      // console.log('Message:', data);
      // if (typeof data === 'object'){
      this.isAlarm = data['alert']
      this.objectsCount = data['object_count']
      // }
    };
  
    ws.onclose = (e) => {
      console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
      this.wsConnect = false;
      setTimeout(() => {
        this.connect();
      }, 1000);
    };
  
    ws.onerror = function(err) {
      console.error('Socket encountered error: ', err, 'Closing socket');
      ws.close();
    };
  }

}
