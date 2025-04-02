export interface iTestInterface
{
    id:number;
    value: string | null;
}
export interface TestUser
{
    userId: number;
    ud: number;
    title: string;
    completed: boolean;
}
export interface TestPost
{
    id: number;
    title: string;
    path: string;
}
export class TestPostClass implements TestPost
{
    id!: number;
    title!:string;
    path!:string;
    back:string | null = null;

    public doSomething():void
    {
        this.path = "dd";
    }
}