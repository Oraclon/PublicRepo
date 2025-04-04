import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { SessionService } from './services/sessionService.service';

export const authGuardGuard: CanActivateFn = (route, state) => {
  let session: SessionService = inject(SessionService);
  return session.checkLogin();
};
