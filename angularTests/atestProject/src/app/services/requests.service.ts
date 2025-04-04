import { HttpClient } from "@angular/common/http";
import { TestPostClass } from "../interfaces/interfaces";
import { Observable, of } from "rxjs";
import { Injectable } from "@angular/core";

@Injectable()
export class ReqService
{
    constructor(private http: HttpClient){}

    controllers = {
        demo: "https://my-json-server.typicode.com/JSGund/XHR-Fetch-Request-JavaScript/posts"
    }
    
    getDemoData():Observable<TestPostClass[]>
    {
        return this.http.get<TestPostClass[]>(this.controllers.demo, {});
    }
}