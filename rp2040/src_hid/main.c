

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "bsp/board_api.h"
#include "tusb.h"

#include "usb_descriptors.h"

#ifndef _TUSB_HID_H_
  #include "hid.h"
#endif
#include "tusb_config.h"

#include "hardware/gpio.h"

#define BUTTON_PIN 17
#define RPI_PIN 15

//--------------------------------------------------------------------+
// MACRO CONSTANT TYPEDEF PROTYPES
//--------------------------------------------------------------------+

/* Blink pattern
* - 250 ms  : device not mounted
* - 1000 ms : device mounted
* - 2500 ms : device is suspended
*/
enum  {
  BLINK_NOT_MOUNTED = 100,
  BLINK_MOUNTED = 500,
  BLINK_SUSPENDED = 2500,
  BUTTON = 1000,
};



static uint32_t blink_interval_ms = BLINK_NOT_MOUNTED;

void led_blinking_task(void);
void hid_task(void);
static bool print_hid(const char* str, int *index_processed);
void handle_button_task();
void handle_rpi_task();
static int button_state = 0;





void sleep(uint32_t ms) {
  uint32_t till = ms + board_millis();
  while (till > board_millis())
  {
    tud_task();
    led_blinking_task();
    handle_button_task();
    handle_rpi_task();
  }
  
}


/*------------- MAIN -------------*/
int main(void)
{
  board_init();

  tud_init(BOARD_TUD_RHPORT);

  gpio_init(BUTTON_PIN);
  gpio_set_dir(BUTTON_PIN, GPIO_IN);
  gpio_pull_up(BUTTON_PIN);

  gpio_init(RPI_PIN);
  gpio_set_dir(RPI_PIN, GPIO_IN);
  gpio_pull_down(RPI_PIN);


  if (board_init_after_tusb) {
    board_init_after_tusb();
  }

  static bool stringDone = false;

  while (1)
  {
    tud_task();
    led_blinking_task();
    hid_task();
    handle_button_task();
    handle_rpi_task();
  }
}


void tud_mount_cb(void)
{
  blink_interval_ms = BLINK_MOUNTED;
}

void tud_umount_cb(void)
{
  blink_interval_ms = BLINK_NOT_MOUNTED;
}

void tud_suspend_cb(bool remote_wakeup_en)
{
  (void) remote_wakeup_en;
  blink_interval_ms = BLINK_SUSPENDED;
}

void tud_resume_cb(void)
{
  blink_interval_ms = tud_mounted() ? BLINK_MOUNTED : BLINK_NOT_MOUNTED;
}

uint8_t const conv_table[128][2] =  { HID_ASCII_TO_KEYCODE };

static bool print_blocking(const char* str) {
  uint8_t keycode[6] = { 0 };
  uint8_t empty_code[6] = {0};
  uint8_t modifier;
  for (int i = 0; i < strlen(str); i++) {
    keycode[0] = conv_table[str[i]][1];
    modifier = 0;
    if ( conv_table[str[i]][0] ) modifier = KEYBOARD_MODIFIER_LEFTSHIFT;
    tud_hid_keyboard_report(REPORT_ID_KEYBOARD, modifier, keycode);
    sleep(5);
    tud_hid_keyboard_report(REPORT_ID_KEYBOARD, 0, empty_code);
    sleep(5);
  }
}



void handle_button_task() {
  if (!gpio_get(BUTTON_PIN)) {
    button_state = true;
  }
}

void handle_rpi_task() {
  if (gpio_get(RPI_PIN)) {
    button_state = true;
  }
}

void hid_task(void)
{
  const uint32_t interval_ms = 5000;
  static uint32_t start_ms = 0;

  // if ( board_millis()) return;
  // start_ms += interval_ms;
  if (button_state) {
    uint32_t last_blink = blink_interval_ms;
    blink_interval_ms = BUTTON;

    print_blocking(";1111111111111111=22223344556677500001?\n");
    button_state = !button_state;
    blink_interval_ms = last_blink;

  }


}


void tud_hid_report_complete_cb(uint8_t instance, uint8_t const* report, uint16_t len)
{

}

uint16_t tud_hid_get_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{ 
  return 0;
}

void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize)
{
  (void) instance;

  if (report_type == HID_REPORT_TYPE_OUTPUT)
  {
    if (report_id == REPORT_ID_KEYBOARD)
    {
      if ( bufsize < 1 ) return;

      uint8_t const kbd_leds = buffer[0];

      if (kbd_leds & board_button_read())
      {
        blink_interval_ms = 0;
        board_led_write(true);
      }else
      {
        board_led_write(false);
        blink_interval_ms = BLINK_MOUNTED;
      }
    }
  }
}

void led_blinking_task(void)
{
  static uint32_t start_ms = 0;
  static bool led_state = false;

  // blink is disabled
  if (!blink_interval_ms) return;

  // Blink every interval ms
  if ( board_millis() - start_ms < blink_interval_ms) return; // not enough time
  start_ms += blink_interval_ms;

  board_led_write(led_state);
  led_state = 1 - led_state; // toggle
}