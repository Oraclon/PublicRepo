import { Component, computed, effect, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

@Component({
  selector: 'app-receive-sarray',
  standalone: false,
  templateUrl: './receive-sarray.component.html',
  styleUrl: './receive-sarray.component.scss'
})
export class ReceiveSarrayComponent {
  constructor(private ms: MainService){
    effect(()=>{ console.log("Added: " + ms.arraySignal()) })
  }

  items: Signal<string[]> = computed(()=>{
    return this.ms.arraySignal();
  }) 

}
