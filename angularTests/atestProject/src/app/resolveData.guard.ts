import { ActivatedRouteSnapshot, ResolveFn, RouterStateSnapshot } from "@angular/router";
import { MainService } from "./services/mainService.service";
import { inject } from "@angular/core";
import { TestPostClass } from "./interfaces/interfaces";
import { ReqService } from "./services/requests.service";

export const productResolver: ResolveFn<void> = (
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
)=>{
    let signals: MainService = inject(MainService);
    let requests: ReqService = inject(ReqService);

    signals.httpSignal.set([]);
    requests.getDemoData().subscribe((response: TestPostClass[])=>{ signals.httpSignal.set(response); });
}