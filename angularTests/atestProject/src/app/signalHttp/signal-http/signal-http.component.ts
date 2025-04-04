import { Component, computed, Signal } from '@angular/core';
import { TestPostClass } from '../../interfaces/interfaces';
import { MainService } from '../../services/mainService.service';
import { ReqService } from '../../services/requests.service';

@Component({
  selector: 'app-signal-http',
  standalone: false,
  templateUrl: './signal-http.component.html',
  styleUrl: './signal-http.component.scss'
})
export class SignalHttpComponent{
  constructor(private ms: MainService, private rq: ReqService){}
  isLogged: Signal<boolean> = computed(()=>{ return this.ms.loginSignal(); });
  totals:Signal<number> = computed(()=>{ return this.ms.httpSignal().length; });
  
  intervalCounter: Signal<number> = computed(()=>{
    return this.ms.intervalSignal();
  });

  getUserData():void
  {
    if(this.ms.loginSignal())
    {
      this.ms.httpSignal.set([]);
      this.rq.getDemoData().subscribe((response: TestPostClass[])=>{ this.ms.httpSignal.set(response); })
    }
  }  
  
}
