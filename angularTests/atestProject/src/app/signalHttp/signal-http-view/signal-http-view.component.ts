import { Component, computed, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { TestPostClass } from '../../interfaces/interfaces';

@Component({
  selector: 'app-signal-http-view',
  standalone: false,
  templateUrl: './signal-http-view.component.html',
  styleUrl: './signal-http-view.component.scss'
})
export class SignalHttpViewComponent {
  constructor(private ms: MainService){}
  isLogged: Signal<boolean> = computed(()=>{
    return this.ms.loginSignal();
  })
  
  items:Signal<TestPostClass[]> = computed(()=>{ return this.ms.httpSignal(); });

  anAction(item: TestPostClass)
  {
    if(item.back == null)
      item.back = item.title;

    item.title = item.title == "" ? item.back : "";
  }
}
