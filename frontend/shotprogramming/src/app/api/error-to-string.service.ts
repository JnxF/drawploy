import {Injectable} from '@angular/core';
import {HttpErrorResponse} from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class ErrorToStringService {
    public errorToString(error: any): string {
        if (error instanceof HttpErrorResponse) {
            switch (error.status) {
                case 500:
                    console.error(error);
                    return 'Error interno del servidor';
                case 401:
                    return 'No autorizado.';
                case 0:
                    if (error.error instanceof ProgressEvent) {
                        const xmlHttp: XMLHttpRequest = error.error.currentTarget as XMLHttpRequest;
                        if (xmlHttp.timeout) {
                            return 'Tiempo máximo de conexión superado, por favor compruebe su conexión a internet';
                        }
                    }
                    if (navigator && navigator.onLine === false) {
                        return 'Error: no dispone de conexión a internet.';
                    }
                    console.error(error);
                    return 'Error desconocido, por favor compruebe su conexión a internet.';
                default:
                    const description = error.error["hydra:description"];
                    if (description) {
                        const result = /^\[KnownError:(\d+)]/.exec(description);
                        if (result) {
                            const str = ErrorToStringService.sTranslateKnownError(result[1]);
                            if (str) {
                                return str;
                            }
                        }
                        console.error(error);
                        return description;
                    }
            }
        }
        console.error(error);
        return 'Error desconocido.';
    }

    private static sTranslateKnownError(errorCode?: string): string {
        if (!errorCode) {
            return null;
        }
        switch (errorCode) {
            case '1451':
                return 'No se puede eliminar el elemento porque existen asociaciones con otros elementos que lo impiden.';
            case '1062':
                return 'El elemento no pudo ser insertado: clave duplicada.';
        }
        return null;
    }
}
