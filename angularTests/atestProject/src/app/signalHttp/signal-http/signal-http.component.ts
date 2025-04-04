import { HttpClient } from '@angular/common/http';
import { Component, computed, OnInit, Signal } from '@angular/core';
import { TestPost, TestPostClass } from '../../interfaces/interfaces';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-signal-http',
  standalone: false,
  templateUrl: './signal-http.component.html',
  styleUrl: './signal-http.component.scss'
})
export class SignalHttpComponent{
  constructor(private http: HttpClient, private ms: MainService){}
  isLogged: Signal<boolean> = computed(()=>{ return this.ms.loginSignal(); })
  totals:Signal<number> = computed(()=>{ return this.ms.httpSignal().length; });
  intervalCounter: Signal<number> = computed(()=>{
    return this.ms.intervalSignal();
  })
  getUserData():void
  {
    if(this.ms.loginSignal())
      this.http.get<TestPostClass[]>("https://my-json-server.typicode.com/JSGund/XHR-Fetch-Request-JavaScript/posts",{})
    .subscribe((response: TestPostClass[])=>{ this.ms.httpSignal.set(response); })
  }  
  
}
