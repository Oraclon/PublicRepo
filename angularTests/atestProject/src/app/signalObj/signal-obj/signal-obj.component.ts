import { Component, computed, effect, ElementRef, Renderer2, Signal, ViewChild } from '@angular/core';
import { MainService } from '../../services/mainService.service';
import { iTestInterface } from '../../interfaces/interfaces';

@Component({
  selector: 'app-signal-obj',
  standalone: false,
  templateUrl: './signal-obj.component.html',
  styleUrl: './signal-obj.component.scss'
})
export class SignalObjComponent {
  constructor(private ms:MainService, private rend: Renderer2){
    /*effect(()=>{ 
      if(ms.arraySignal()){ console.log("Change Made in ArraySignal: " + ms.arraySignal() ) }
    })*/
  }
  @ViewChild("testInput") testInput !: ElementRef;

  value: Signal<iTestInterface> = computed(()=>{
    return this.ms.testSignal();
  });

  getInputValue(el:HTMLInputElement):void
  {
    let val = setInterval(()=>{
      this.ms.testSignal().value = el.value;
      clearInterval(val);
    }, 100)
  }
  increaseId():void
  {
    let a : iTestInterface = this.ms.testSignal();
    a.id++;
    this.ms.testSignal.set(a);
  }
  resetId():void
  {
    this.ms.testSignal().id = 0;
  }
  clearText():void
  {
    this.ms.testSignal().value = null;
    this.rend.setProperty(this.testInput.nativeElement, "value", null);
  }
}
