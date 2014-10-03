#include "descriptors.h"

#if !(USB_VID + 0)
#error "Define an environment variable named USB_VID that contains the usb vendor id"
#endif

#if !(USB_PID + 0)
#error "Define an environment variable named USB_PID that contains the usb product id"
#endif

#define STR_(x) #x
#define STR(x) STR_(x)

#define LSTR_(x) L""#x
#define LSTR(x) LSTR_(x)

#define STRLEN(x) strlen(x)

/** Device descriptor structure. This descriptor, located in FLASH memory, describes the overall
 *  device characteristics, including the supported USB version, control endpoint size and the
 *  number of device configurations. The descriptor is read out by the USB host when the enumeration
 *  process begins.
 */
const USB_Descriptor_Device_t PROGMEM XLink_DeviceDescriptor =
{
	.Header                 = {.Size = sizeof(USB_Descriptor_Device_t), .Type = DTYPE_Device},

	.USBSpecification       = VERSION_BCD(01.10),
	.Class                  = USB_CSCP_VendorSpecificClass,
	.SubClass               = USB_CSCP_NoDeviceSubclass,
	.Protocol               = USB_CSCP_NoDeviceProtocol,

	.Endpoint0Size          = FIXED_CONTROL_ENDPOINT_SIZE,

	.VendorID               = USB_VID,
	.ProductID              = USB_PID,
	.ReleaseNumber          = VERSION_BCD(01.00),

	.ManufacturerStrIndex   = STRING_ID_Manufacturer,
	.ProductStrIndex        = STRING_ID_Product,
	.SerialNumStrIndex      = STRING_ID_Serial,

	.NumberOfConfigurations = FIXED_NUM_CONFIGURATIONS
};

/** Configuration descriptor structure. This descriptor, located in FLASH memory, describes the usage
 *  of the device in one of its supported configurations, including information about any device interfaces
 *  and endpoints. The descriptor is read out by the USB host during the enumeration process when selecting
 *  a configuration so that the host may correctly communicate with the USB device.
 */
const USB_Descriptor_Configuration_t PROGMEM XLink_ConfigurationDescriptor =
{
	.Config =
		{
			.Header                 = {.Size = sizeof(USB_Descriptor_Configuration_Header_t), .Type = DTYPE_Configuration},

			.TotalConfigurationSize = sizeof(USB_Descriptor_Configuration_t),
			.TotalInterfaces        = 1,

			.ConfigurationNumber    = 1,
			.ConfigurationStrIndex  = NO_DESCRIPTOR,

			.ConfigAttributes       = USB_CONFIG_ATTR_RESERVED,

			.MaxPowerConsumption    = USB_CONFIG_POWER_MA(100)
		},

	.XLinkInterface =
		{
			.Header                 = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},

			.InterfaceNumber        = 0,
			.AlternateSetting       = 0,

			.TotalEndpoints         = 0,

			.Class                  = USB_CSCP_VendorSpecificClass,
			.SubClass               = 0x00,
			.Protocol               = 0x00,

			.InterfaceStrIndex      = NO_DESCRIPTOR
		},
};

/** Language descriptor structure. This descriptor, located in FLASH memory, is returned when the host requests
 *  the string descriptor with index 0 (the first index). It is actually an array of 16-bit integers, which indicate
 *  via the language ID table available at USB.org what languages the device supports for its string descriptors.
 */
const USB_Descriptor_String_t PROGMEM XLink_LanguageString =
{
  .Header        = {.Size = USB_STRING_LEN(1), .Type = DTYPE_String},
  
  .UnicodeString = {LANGUAGE_ID_ENG}
};

/** Manufacturer descriptor string. This is a Unicode string containing the manufacturer's details in human readable
 *  form, and is read out upon request by the host when the appropriate string ID is requested, listed in the Device
 *  Descriptor.
 */
const USB_Descriptor_String_t PROGMEM XLink_ManufacturerString =
{
  .Header        = {.Size = USB_STRING_LEN(8), .Type = DTYPE_String},

  .UnicodeString = L"XLink"
};

/** Product descriptor string. This is a Unicode string containing the product's details in human readable form,
 *  and is read out upon request by the host when the appropriate string ID is requested, listed in the Device
 *  Descriptor.
 */
const USB_Descriptor_String_t PROGMEM XLink_ProductString =
{
  .Header        = {.Size = USB_STRING_LEN(7), .Type = DTYPE_String},

  .UnicodeString = L"USB Adapter"
};

/** Serial number string. This is a Unicode string containing the device's unique serial number, expressed as a
 *  series of uppercase hexadecimal digits.
 */
const USB_Descriptor_String_t PROGMEM XLink_SerialString =
{
  .Header        = {.Size = USB_STRING_LEN(STRLEN(STR(USB_SERIAL))), .Type = DTYPE_String},

  .UnicodeString = LSTR(USB_SERIAL)
};

/** This function is called by the library when in device mode, and must be overridden (see library "USB Descriptors"
 *  documentation) by the application code so that the address and size of a requested descriptor can be given
 *  to the USB library. When the device receives a Get Descriptor request on the control endpoint, this function
 *  is called so that the descriptor details can be passed back and the appropriate descriptor sent back to the
 *  USB host.
 */
uint16_t CALLBACK_USB_GetDescriptor(const uint16_t wValue,
                                    const uint8_t wIndex,
                                    const void** const DescriptorAddress)
{
	const uint8_t  DescriptorType   = (wValue >> 8);
	const uint8_t  DescriptorNumber = (wValue & 0xFF);

	const void* Address = NULL;
	uint16_t    Size    = NO_DESCRIPTOR;

	switch (DescriptorType)
	{
		case DTYPE_Device:
			Address = &XLink_DeviceDescriptor;
			Size    = sizeof(USB_Descriptor_Device_t);
			break;
		case DTYPE_Configuration:
			Address = &XLink_ConfigurationDescriptor;
			Size    = sizeof(USB_Descriptor_Configuration_t);
			break;
		case DTYPE_String:
			switch (DescriptorNumber)
			{
				case STRING_ID_Language:
					Address = &XLink_LanguageString;
					Size    = pgm_read_byte(&XLink_LanguageString.Header.Size);
					break;
				case STRING_ID_Manufacturer:
					Address = &XLink_ManufacturerString;
					Size    = pgm_read_byte(&XLink_ManufacturerString.Header.Size);
					break;
				case STRING_ID_Product:
					Address = &XLink_ProductString;
					Size    = pgm_read_byte(&XLink_ProductString.Header.Size);
					break;
				case STRING_ID_Serial:
					Address = &XLink_SerialString;
					Size    = USB_STRING_LEN(STRLEN(STR(USB_SERIAL)));
					break;
			}

			break;
	}

	*DescriptorAddress = Address;
	return Size;
}

