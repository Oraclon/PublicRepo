import { Component, computed, effect, OnInit, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { iTestInterface } from '../../interfaces/interfaces';

@Component({
  selector: 'app-receive-obj',
  standalone: false,
  templateUrl: './receive-obj.component.html',
  styleUrl: './receive-obj.component.scss'
})
export class ReceiveObjComponent{
  constructor(private ms:MainService){
    effect(()=>{ console.log(this.ms.testSignal()) })
  }
  value: Signal<iTestInterface> = computed(()=>{
    return this.ms.testSignal();
  })

}
