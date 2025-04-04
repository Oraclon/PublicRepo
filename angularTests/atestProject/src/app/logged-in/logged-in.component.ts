import { Component, computed, Signal } from '@angular/core';
import { MainService } from '../services/mainService.service';
import { TestPostClass } from '../interfaces/interfaces';

@Component({
  selector: 'app-logged-in',
  standalone: false,
  templateUrl: './logged-in.component.html',
  styleUrl: './logged-in.component.scss'
})
export class LoggedInComponent{
  constructor(private ms: MainService){}
  items: Signal<TestPostClass[]> = computed(()=>{ return this.ms.httpSignal(); })
}
