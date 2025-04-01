import { Component, computed, OnInit, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-signal-read',
  standalone: false,
  templateUrl: './signal-read.component.html',
  styleUrl: './signal-read.component.scss'
})
export class SignalReadComponent{
  constructor(private ms: MainService){}
 
  mainCounter:Signal<number> = computed(()=>{
    return this.ms.sig();
  });
  derivedCounter:Signal<number> = computed(()=>{
    return this.ms.sig() * 10;
  });
  
  reset():void
  {
    this.ms.sig.set(0);
  }
}
