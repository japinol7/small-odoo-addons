# Release History

## v19.1.1.1

### Features upgraded for Odoo 19.0

* Several improvements to this addon:
  * jap_simple_bulk_server_job

* Minor improvements to this addon:
  * jap_sale

<br>

## v19.1.1.0

### Features added and upgraded for Odoo 19.0

* New Addons:
  * jap_simple_bulk_server_job

* Addons Improved:
  * jap_addons_config
  * jap_custom_security
  * jap_customize_version
  * jap_sale


#### About the new addon:

'JAP Simple Bulk Server Job' is a Technical addon intended to be used by System Administrators.

This addon allows creating special jobs able to process several records in bulk; 
a batch of N items per cron execution. 

It includes a Wizard to create jobs, views to manage them and a cron to execute the jobs.
* All the menus and views can be accessed from this menu:
Settings -- Technical -- Jap. Addons

<br>

## v19.1.0.0

### Features upgraded to Odoo 19

* Addons upgraded:
  * jap_addons_config
  * jap_custom_security
  * jap_customize_version
  * jap_sale

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for users with the group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br />
  * One letter A within a solid circle.

* Create an Invoice from Selected Sale Lines.
  * Only visible for users with the group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.

* Open an order of the same customer using a wizard that displays a list of all sales <br /> orders associated with the customer of the current order.

* Customize the JAP addons version using the addon:
  * jap_customize_version.

<br>

## v18.1.0.0

### Features upgraded to Odoo 18

* Add an addon to customize JAP addons version.
  * jap_customize_version.
* Improve addon jap_sale:
  * When copying a line, set the qty to 0 instead of 1.
  * Add wizard that displays a list of all sales orders associated <br /> with the customer of the current order
* Some minor improvements.

<br>

## v18.0.1.0

### Features upgraded to Odoo 18

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for user with group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br />
  * One letter A within a solid circle.

* Create an Invoice from Selected Sale Lines.
  * Only visible for user with group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.

<br>

## v17.0.1.0 

### Features upgraded to Odoo 17

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for user with group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br /> 
  * One letter A within a solid circle. 

* Create an Invoice from Selected Sale Lines.
  * Only visible for user with group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.

<br>

## v16.0.1.0 

## Odoo new addon: JAP Sales

### New Features

* Duplicate a sale line with the duplication button <br /> on the right side of the line.
  * Only visible for user with group: Sale Duplicate Lines.
  * Users with the group 'Role Sales Squad' inherit this group.

* Duplicated lines will be marked with this icon on the most important views: <br /> 
  * One letter A within a solid circle. 

* Create an Invoice from Selected Sale Lines.
  * Only visible for user with group: Role Sales Squad.
  * You can select which lines to invoice.
  * You can also add an Invoice note that will be added to the created invoice.

### Notes
  * These addons are compatible with Odoo 16.0.
