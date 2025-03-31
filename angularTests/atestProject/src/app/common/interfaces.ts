export interface iSelection
{
    id: number | null;
    value: string;
    description: string | null;
    selected: boolean;
}

export class SelectionItem implements iSelection
{
    id!: number | null;
    value!: string;
    description!: string | null;
    selected: boolean = false;

    constructor(public item:iSelection)
    {
        Object.assign(this, item);
    }

    changeStatus():void
    {
        this.selected = !this.selected;
    }
} 

export class SelectionItemsBlock
{
    data: SelectionItem[] = [];
    selections: SelectionItem[] = [];

    constructor(data: iSelection[])
    {
        let generated: SelectionItem[] = [];
        for(let x: number = 0; x < data.length; x++)
            generated.push(new SelectionItem(data[x]));
        this.data = generated;
    }

    addToSelections(item: SelectionItem):void
    {
        item.changeStatus();
        item.selected ? this.selections.push(item) : this._removeFromSelections(item);
    }

    clearSelections():void
    {
        this.data.map((x:SelectionItem)=> {x.selected = false; return x;});
        this.selections = [];
    }

    private _removeFromSelections(item: SelectionItem): void
    {
        let knownIndex: number = 0;
        for(let x: number = 0; x < this.selections.length; x++)
            if(this.selections[x].value == item.value)
            {
                knownIndex = x;
                break;
            }
        this.selections.splice(knownIndex, 1);
    }

    set value (value: string | null)
    {
        if(value != null)
        {
            let container = value.split("-");
            for(let x: number = 0; x < this.data.length; x++)
                if(container.includes(this.data[x].value))
                {
                    this.data[x].selected = true;
                    this.selections.push(this.data[x]);
                }            
        }
    }
    get value(): string | null
    {
       return this.selections.length == 0 ? null : this.selections.map(x=> x.value).join(","); 
    }
}