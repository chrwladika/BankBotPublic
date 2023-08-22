import {Component, OnInit} from '@angular/core';
import {interval, Subscription} from "rxjs";
import {CommServiceService} from "../service/comm-service.service";
import {Page} from "../interfaces/page";
import {CSRequest} from "../interfaces/csrequest";

@Component({
  selector: 'app-cs',
  templateUrl: './cs.component.html',
  styleUrls: ['./cs.component.scss']
})
// CsComponent class
export class CsComponent implements OnInit {
  items: CSRequest[] = [];
  categories = ['Card', 'General', 'Credit'];
  selectedCategory: string | null = null;
  page: number = 1;
  polling: Subscription | null | undefined;
  maximumPages: number = 1;

  // Constructor
  constructor(private commservice: CommServiceService) {}

  // OnInit lifecycle hook
  ngOnInit(): void {
    this.fetchItems();
  }

  // Fetch items function
  fetchItems(): void {
    this.commservice.fetchItems(this.selectedCategory, this.page).subscribe(data => {
      const pageData: Page = data.page as Page; // Casting the data to Page type
      console.log(data);
      this.items = pageData.pageContents;

      // Update the current page and maximum pages
      this.page = pageData.pageNumber;
      this.maximumPages = pageData.maximumPages;

      if (this.items.length < 8 && !this.polling) {
        this.polling = interval(10000).subscribe(() => this.fetchItems());
      } else if (this.items.length >= 8 && this.polling) {
        this.polling.unsubscribe();
        this.polling = null;
      }
    });
  }

  // onCategoryChange function
  onCategoryChange(category: string): void {
    this.selectedCategory = category || null;
    this.fetchItems();
  }

  // onPageChange function
  onPageChange(page: number): void {
    this.page = page;
    this.fetchItems();
  }


}
