import { Component, OnInit } from '@angular/core';
import { SelectionItem, iSelection, SelectionItemsBlock } from '../common/interfaces';

@Component({
  selector: 'app-acomponent',
  standalone: false,
  templateUrl: './acomponent.component.html',
  styleUrl: './acomponent.component.scss'
})

export class AcomponentComponent implements OnInit{
    items: iSelection[] = [...Array(20).keys()].map((x:number)=> ({id: x, value: x.toString(), description:`desc-${x}` } as iSelection));
    selectionsBlock: SelectionItemsBlock = new SelectionItemsBlock(this.items);
  
    ngOnInit(): void {
      this.selectionsBlock.value = "2-4-5-6";
    }

    changeSelection(item:SelectionItem):void
    {
      this.selectionsBlock.addToSelections(item); 
    }
    clearSelections():void
    {
      this.selectionsBlock.clearSelections();
    }
}
