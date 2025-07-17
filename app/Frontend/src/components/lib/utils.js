import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Combines multiple class name strings and merges Tailwind classes
 * @param {string[]} inputs - class name strings
 * @returns {string} - merged class names
 */
export function cn(...inputs) {
  return twMerge(clsx(inputs))
}
