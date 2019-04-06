import {Injectable} from '@angular/core';
import {HttpErrorResponse} from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class ErrorToStringService {
    public errorToString(error: any): string {
        if (error instanceof HttpErrorResponse) {
          if (error.status != 0) {
            return error.message;
          }
        }
        console.error(error);
        return 'Unknown error.';
    }
}
