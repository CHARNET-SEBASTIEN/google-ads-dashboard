import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'numberFormat',
  standalone: true
})
export class NumberFormatPipe implements PipeTransform {
  transform(value: number | string | null | undefined, decimals: number = 0): string {
    if (value === null || value === undefined || value === '') {
      return '0';
    }

    const num = typeof value === 'string' ? parseFloat(value) : value;

    if (isNaN(num)) {
      return '0';
    }

    // Format with specified decimals
    const formatted = num.toFixed(decimals);

    // Split into integer and decimal parts
    const parts = formatted.split('.');
    const integerPart = parts[0];
    const decimalPart = parts[1];

    // Add space as thousand separator
    const withSpaces = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

    // Return with decimal part if exists
    return decimalPart ? `${withSpaces},${decimalPart}` : withSpaces;
  }
}
