import { Injectable } from '@angular/core';
import { Subject, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DiagnosticService {
  private refreshSubject = new Subject<void>();
  refresh$ = this.refreshSubject.asObservable();

  // Track if Drive is configured
  private driveConfiguredSubject = new BehaviorSubject<boolean>(false);
  driveConfigured$ = this.driveConfiguredSubject.asObservable();

  triggerRefresh() {
    this.refreshSubject.next();
  }

  setDriveConfigured(configured: boolean) {
    this.driveConfiguredSubject.next(configured);
  }
}
