// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from raspimouse_msgs:msg/Leds.idl
// generated code does not contain a copyright notice
#include "raspimouse_msgs/msg/detail/leds__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "raspimouse_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "raspimouse_msgs/msg/detail/leds__struct.h"
#include "raspimouse_msgs/msg/detail/leds__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _Leds__ros_msg_type = raspimouse_msgs__msg__Leds;

static bool _Leds__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Leds__ros_msg_type * ros_message = static_cast<const _Leds__ros_msg_type *>(untyped_ros_message);
  // Field name: led0
  {
    cdr << (ros_message->led0 ? true : false);
  }

  // Field name: led1
  {
    cdr << (ros_message->led1 ? true : false);
  }

  // Field name: led2
  {
    cdr << (ros_message->led2 ? true : false);
  }

  // Field name: led3
  {
    cdr << (ros_message->led3 ? true : false);
  }

  return true;
}

static bool _Leds__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Leds__ros_msg_type * ros_message = static_cast<_Leds__ros_msg_type *>(untyped_ros_message);
  // Field name: led0
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->led0 = tmp ? true : false;
  }

  // Field name: led1
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->led1 = tmp ? true : false;
  }

  // Field name: led2
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->led2 = tmp ? true : false;
  }

  // Field name: led3
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->led3 = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_raspimouse_msgs
size_t get_serialized_size_raspimouse_msgs__msg__Leds(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Leds__ros_msg_type * ros_message = static_cast<const _Leds__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name led0
  {
    size_t item_size = sizeof(ros_message->led0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name led1
  {
    size_t item_size = sizeof(ros_message->led1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name led2
  {
    size_t item_size = sizeof(ros_message->led2);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name led3
  {
    size_t item_size = sizeof(ros_message->led3);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Leds__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_raspimouse_msgs__msg__Leds(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_raspimouse_msgs
size_t max_serialized_size_raspimouse_msgs__msg__Leds(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: led0
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: led1
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: led2
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: led3
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = raspimouse_msgs__msg__Leds;
    is_plain =
      (
      offsetof(DataType, led3) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Leds__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_raspimouse_msgs__msg__Leds(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Leds = {
  "raspimouse_msgs::msg",
  "Leds",
  _Leds__cdr_serialize,
  _Leds__cdr_deserialize,
  _Leds__get_serialized_size,
  _Leds__max_serialized_size
};

static rosidl_message_type_support_t _Leds__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Leds,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, raspimouse_msgs, msg, Leds)() {
  return &_Leds__type_support;
}

#if defined(__cplusplus)
}
#endif
