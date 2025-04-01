import { Component, computed, Signal } from '@angular/core';
import { MainService } from '../../services/mainService.service';

export enum ViewType
{
  None,
  View1,
  View2,
  View3
}

@Component({
  selector: 'app-view-update',
  standalone: false,
  templateUrl: './view-update.component.html',
  styleUrl: './view-update.component.scss'
})

export class ViewUpdateComponent {
  constructor(private ms: MainService){}
  viewType: typeof ViewType = ViewType;
  view: Signal<ViewType> = computed(()=>{
    return this.ms.viewSignal();
  });
}
