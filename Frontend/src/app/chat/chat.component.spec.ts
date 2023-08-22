import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatComponent } from './chat.component';

describe('ChatComponent', () => {
  let component: ChatComponent;
  let fixture: ComponentFixture<ChatComponent>;

  /**
   * Configure the testing module and create a component fixture.
   */
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ChatComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ChatComponent);
    component = fixture.componentInstance;

    // Trigger the change detection cycle to initialize the component
    fixture.detectChanges();
  });

  /**
   * Test whether the ChatComponent is created successfully.
   */
  it('should create', () => {
    // The 'expect' statement asserts that the component instance is truthy
    expect(component).toBeTruthy();
  });
});
