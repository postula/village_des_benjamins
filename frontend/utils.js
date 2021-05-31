import {DateTime} from "luxon";

export const formatDate = d => DateTime.fromISO(d).toLocaleString(DateTime.DATE_FULL);
export const formatTime = d => DateTime.fromISO(d).toLocaleString(DateTime.TIME_24_SIMPLE);
