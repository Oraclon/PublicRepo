import { Component, computed, effect, OnInit, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { iTestInterface } from '../../interfaces/interfaces';
import { interval, Observable, take } from 'rxjs';

@Component({
  selector: 'app-receive-obj',
  standalone: false,
  templateUrl: './receive-obj.component.html',
  styleUrl: './receive-obj.component.scss'
})
export class ReceiveObjComponent implements OnInit{

  numbers: Observable<number> = interval(1000).pipe(take(20));
  ngOnInit(): void {
    this.numbers.subscribe((x:number)=>this.ms.intervalSignal.set(x+1) )
  }

  constructor(private ms:MainService){
    //effect(()=>{ console.log(this.ms.testSignal()) })
  }
  value: Signal<iTestInterface> = computed(()=>{
    return this.ms.testSignal();
  })
}
